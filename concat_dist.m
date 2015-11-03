clc;
clear;
addpath(genpath('~/HMMall'));
load('Datasets/processed/dist_readings.mat');

models_count = size(acc_mapped_to_codebook,2);
primitives = 8;
concats = models_count - primitives;
%concats = 0;
used_models = models_count;

train_set = acc_mapped_to_codebook(1,1:primitives);
test_set = acc_mapped_to_codebook(1,primitives+1:models_count);


% Prepare HMM
Q = 8;
O = 32;
max_iter = 10;

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

transmat= zeros (Q, Q,size(train_set,2));
obsmat  = zeros(Q, O,size(train_set,2));
LL 		= zeros (1, max_iter, size(train_set,2));
prior	= zeros (Q,1, size(train_set,2));

% Train primitive models
for i=1:size(train_set,2)
	[LL, prior(:,1,i), transmat(:,:,i), obsmat(:,:,i)] = dhmm_em(train_set{1,i,:}, prior1, transmat1, obsmat1, 'max_iter', max_iter);
end


%%%%%%%%%%%%%%%%%%% Construct square l-d-r-u HMM %%%%%%%%%%%%%%%%%%%%%%
% Construct the transmat (1,3,2,4)
transmat_squarel = blkdiag(transmat(:,:,1), transmat(:,:,3), transmat(:,:,2), transmat(:,:,4));
	% Update transmat at model transition
	for i=1:3 % As we have 3 transitions between 4 models
		transmat_squarel(i*Q,i*Q) = 0;
		transmat_squarel(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (1,3,2,4)
obsmat_squarel = vertcat(obsmat(:,:,1), obsmat(:,:,3), obsmat(:,:,2), obsmat(:,:,4));
% Construct the prior
prior_squarel = zeros (1, 4*Q);
prior_squarel (1,1) = 1;

%%%%%%%%%%%%%%%%%%% Construct square r-d-l-u HMM %%%%%%%%%%%%%%%%%%%%%%
% Construct the transmat (2,3,1,4)
transmat_squarer = blkdiag(transmat(:,:,2), transmat(:,:,3), transmat(:,:,1),transmat(:,:,4));
	% Update transmat at model transition
	for i=1:3 % As we have 3 transitions between 4 models
		transmat_squarer(i*Q,i*Q) = 0;
		transmat_squarer(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (2,3,1,4)
obsmat_squarer = vertcat(obsmat(:,:,2), obsmat(:,:,3), obsmat(:,:,1),obsmat(:,:,4));
% Construct the prior
prior_squarer = zeros (1, 4*Q);
prior_squarer (1,1) = 1;

%%%%%%%%%%%%%%%%%%% Construct trianglecw dline-nw-se, hline-left, dline-sw-ne HMM  
% Construct the transmat (6,1,8)
transmat_trianglecw = blkdiag(transmat(:,:,6), transmat(:,:,1), transmat(:,:,8));
	% Update transmat at model transition
	for i=1:2 % As we have 2 transitions between 3 models
		transmat_trianglecw(i*Q,i*Q) = 0;
		transmat_trianglecw(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (6,1,8)
obsmat_trianglecw = vertcat(obsmat(:,:,6), obsmat(:,:,1), obsmat(:,:,8));
% Construct the prior
prior_trianglecw = zeros (1, 3*Q);
prior_trianglecw (1,1) = 1;

%%%%%%%%%%%%%%%%%%% Construct triangle ccw dline-ne-sw, hline-right, dline-se-nw HMM  
% Construct the transmat (5,2,7)
transmat_triangleccw = blkdiag(transmat(:,:,5), transmat(:,:,2), transmat(:,:,7));
	% Update transmat at model transition
	for i=1:2 % As we have 2 transitions between 3 models
		transmat_triangleccw(i*Q,i*Q) = 0;
		transmat_triangleccw(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (5,2,7)
obsmat_triangleccw = vertcat(obsmat(:,:,5), obsmat(:,:,2), obsmat(:,:,7));
% Construct the prior
prior_triangleccw = zeros (1, 3*Q);
prior_triangleccw (1,1) = 1;

%%%%%%%%%%%%%%%%%%% Construct Z (hline-right, diagonal ne-sw,hline-right) HMM  
% Construct the transmat (2,5,2)
transmat_Z = blkdiag(transmat(:,:,2), transmat(:,:,5), transmat(:,:,2));
	% Update transmat at model transition
	for i=1:2 % As we have 2 transitions between 3 models
		transmat_Z(i*Q,i*Q) = 0;
		transmat_Z(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (2,5,2)
obsmat_Z = vertcat(obsmat(:,:,2), obsmat(:,:,5), obsmat(:,:,2));
% Construct the prior
prior_Z = zeros (1, 3*Q);
prior_Z (1,1) = 1;

%%%%%%%%%%%%%%%%%%% Construct tick (dline-nw-se, dline-sw-ne) HMM  
% Construct the transmat (6,8)
transmat_tick = blkdiag(transmat(:,:,6), transmat(:,:,8));
	% Update transmat at model transition
	for i=1:1 % As we have 1 transition between 2 models
		transmat_tick(i*Q,i*Q) = 0;
		transmat_tick(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (6,8)
obsmat_tick = vertcat(obsmat(:,:,6), obsmat(:,:,8));
% Construct the prior
prior_tick = zeros (1, 2*Q);
prior_tick (1,1) = 1;

% Test sets Square, triangle, Z, vs 11 models ; 4 concat models + 7 primitive models
confusion_matrix = zeros(used_models);


% Testing Square, triangle and Z
% Print the number of samples
accuracy_count = 0;
class_count = zeros (1,used_models);
for j = 1 : used_models  % Square is @8, triangle @9, Z @10
	data = [acc_mapped_to_codebook{1,j}];
	class_count(1,j) = size(data,2);
	accuracy_count = accuracy_count + size(data,2);
	for i=1:size(data,2)
		
		likelihood = zeros(1, 8);
		
		% Against the primitive models 7 
		for k =1: primitives % 7 primitive models
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
				prior(:,:,k), transmat(:,:,k), obsmat(:,:,k));
		end

		k = primitives + 1;
		%%%% Against the concat models
		if k <= used_models 
			% Squarel
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_squarel, transmat_squarel, obsmat_squarel);
				k = k + 1;
		end

		if k <= used_models 
			% Squarer
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_squarer, transmat_squarer, obsmat_squarer);
			k = k + 1;
		end

		if k <= used_models 
			% trianglecw
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_trianglecw, transmat_trianglecw, obsmat_trianglecw);
			k = k + 1;
		end

		if k <= used_models 
			% triangleccw
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_triangleccw, transmat_triangleccw, obsmat_triangleccw);
			k = k + 1;
		end
		
		if k <= used_models 
			% Z
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_Z, transmat_Z, obsmat_Z);

			k = k + 1;
		end
		
		if k <= used_models 
			% tick
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_tick, transmat_tick, obsmat_tick);
			
			k = k + 1;
		end
		[val, index] = max(likelihood(:,:));
		
		% Added a check that val is not -Inf, do not add it to the matrix
		if val ~= -Inf
			%index = size (confusion_matrix, 2);
			confusion_matrix(j,index) = confusion_matrix(j,index)+ 1;
		end 
			

	end
end

class_count
Accuracy = trace(confusion_matrix)/sum(sum(confusion_matrix))

