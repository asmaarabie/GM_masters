clc;
clear;
addpath(genpath('~/HMMall'));
%load('Datasets/processed/square_parts_mapped_1431214818.mat');
load('Datasets/processed/square_parts_mapped_filtered_1431654181.mat');
% Python starts indices from 0, matlab from 1. Add 1 to python mat
for i=1:size(acc_mapped_to_codebook,1)
	for j = 1:size(acc_mapped_to_codebook,2)
		acc_mapped_to_codebook{i,j,:} = acc_mapped_to_codebook{i,j,:} +1;
	end
end

% Take all data as training for classes [1:'hline-left', 2:'hline-right', 3:'square', 4:'vline-down', 5:'vline-up']
classes = [1, 2, 4, 5]
train_set = acc_mapped_to_codebook(classes,:,:);

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


% Segment the square manually
% it is 30*41, but due to reshape column major, we are making it 41, 30 then it is going to be transposed
correct = [0,0,0,0];
target = [5,1,4, 2];
confusion_matrix = zeros(5);
for i=1:size(acc_mapped_to_codebook(3,:,:), 2)
	square = cell2mat(acc_mapped_to_codebook(3,i,:));
	segmented_square = zeros (4, floor(size(square,2)/4));
	for j=1:4
		start = (j-1)*floor(size(square,2)/4) + 1; 
		endint = start +floor(size(square,2)/4) -1;
		segmented_square(j, :) = square (1, start:endint); % Misses the last 1~3 entries
	end

	for j=1:size(segmented_square,1) % get number of segments per sample
		likelihood = zeros(1, size(classes,1));
		for k =1:size(classes, 2) 
			likelihood(:,k) = dhmm_logprob(segmented_square(j, :), prior(:,:,k), transmat(:,:,k), obsmat(:,:,k));
		end
		[val, index] = max(likelihood(:,:));
		confusion_matrix(target(j), classes(index)) = confusion_matrix(target(j), classes(index)) +1;
	end
	%disp(identified_as);
end
correct_4_segments = trace (confusion_matrix) / sum(sum(confusion_matrix))
