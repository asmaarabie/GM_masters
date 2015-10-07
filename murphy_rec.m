clc;
clear;
addpath(genpath('~/HMMall'));
load('Datasets/processed/Lines_best_primitives_1438175944');
%load('Datasets/processed/square_parts_mapped_w_1431214818.mat');
% Python starts indices from 0, matlab from 1. Add 1 to python mat
%{
for i=1:size(acc_mapped_to_codebook,1)
	for j = 1:size(acc_mapped_to_codebook,2)
		acc_mapped_to_codebook{i,j,:} = acc_mapped_to_codebook{i,j,:} +1;
	end
end
%}

% Calculate the average of multiple runs of HMM 
runs = 10;
avg_accuracy = 0;
best_accuracy =0;
for r = 1:runs 
	% Divide it into train and test
	% Select 20% of data for training and 80% to find average likelihood. 
	k = 3; % how many folds i want
	N = size(acc_mapped_to_codebook,2);
	indices = crossvalind('Kfold',N,k);

	% Split orignial set
	train = (indices == 1) ; % which points are in the test set
	test= ~train; % all points that are NOT in the test set

	test_set = acc_mapped_to_codebook(:,test,:);
	train_set = acc_mapped_to_codebook(:, train,:);

	% Prepare HMM
	Q = 8;
	O = 8;
	max_iter = 3;

	% initial guess of parameters
	prior1 = zeros(Q,1);
	prior1(1)= 1;
	transmat1 = zeros(Q);
	for i = 1:(Q-1)
	    transmat1(i,i) = 0.5;
	    transmat1(i,i+1) = 0.5;
	end
	transmat1(Q, Q) = 1;
	obsmat1 = ones(Q, O)* (1/O); 

	transmat= zeros (Q, Q,size(train_set,1));
	obsmat  = zeros(Q, O,size(train_set,1));
	LL 		= zeros (1, max_iter, size(train_set,1));
	prior	= zeros (Q,1, size(train_set,1));


	for i=1:size(train_set,1)
		[LL, prior(:,1,i), transmat(:,:,i), obsmat(:,:,i)] = dhmm_em(train_set(i,:,:), prior1, transmat1, obsmat1, 'max_iter', max_iter);
	end

	% use model to compute log likelihood
	%loglik = dhmm_logprob(test_set(1,1), prior2, transmat2, obsmat2)
	% log lik is slightly different than LL(end), since it is computed after the final M step
	confusion_matrix = zeros(size(acc_mapped_to_codebook,1), size(acc_mapped_to_codebook,1));
	likelihood = zeros(1, size(test_set,1));
	for i=1:size(test_set,1)
		for j=1:size(test_set,2)
			likelihood = zeros(1, size(test_set,1));
			for k =1:size(test_set,1)
				likelihood(:,k) = dhmm_logprob(test_set(i,j,:), prior(:,:,k), transmat(:,:,k), obsmat(:,:,k));
			end
			[val, index] = max(likelihood(:,:));
			
			% Added a check that val is not -Inf, do not add it to the matrix
			if val ~= -Inf
				%index = size (confusion_matrix, 2);
				confusion_matrix(i,index) = confusion_matrix(i,index)+ 1;
			end 
			

		end
	end

	% 1:size (confusion_matrix, 1) --> to make sure it is a square matrix
	accuracy = trace (confusion_matrix(:, 1:size (confusion_matrix, 1))) / sum(sum(confusion_matrix));
	avg_accuracy = avg_accuracy+ accuracy;
	best_accuracy = max([accuracy best_accuracy]);
end
(avg_accuracy / runs)*100
best_accuracy*100