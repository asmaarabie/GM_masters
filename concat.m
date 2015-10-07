clc;
clear;
addpath(genpath('~/HMMall'));
load('Datasets/processed/conact_1438175944.mat');

models_count = size(acc_mapped_to_codebook,2);
primitives = 7;
concats = models_count - primitives;

train_set = acc_mapped_to_codebook(1,1:primitives);
test_set = acc_mapped_to_codebook(1,primitives+1:models_count);


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

%%%%%%%%%%%%%%%%%%% Construct square u-l-d-r HMM %%%%%%%%%%%%%%%%%%%%%%
% Construct the transmat (3,2,4,1)
transmat_squareu = blkdiag(transmat(:,:,3), transmat(:,:,2), transmat(:,:,4),transmat(:,:,1));
	% Update transmat at model transition
	for i=1:3 % As we have 3 transitions between 4 models
		transmat_squareu(i*Q,i*Q) = 0;
		transmat_squareu(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (1,3,2,4)
obsmat_squareu = vertcat(obsmat(:,:,3), obsmat(:,:,2), obsmat(:,:,4),obsmat(:,:,1));
% Construct the prior
prior_squareu = zeros (1, 4*Q);
prior_squareu (1,1) = 1;

%%%%%%%%%%%%%%%%%%% Construct triangle (diagonal ne-sw, hline-right, diagonal se-nw) HMM  
% Construct the transmat (5,2,7)
transmat_triangle = blkdiag(transmat(:,:,5), transmat(:,:,2), transmat(:,:,7));
	% Update transmat at model transition
	for i=1:2 % As we have 2 transitions between 3 models
		transmat_triangle(i*Q,i*Q) = 0;
		transmat_triangle(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (5,2,7)
obsmat_triangle = vertcat(obsmat(:,:,5), obsmat(:,:,2), obsmat(:,:,7));
% Construct the prior
prior_triangle = zeros (1, 3*Q);
prior_triangle (1,1) = 1;

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

%%%%%%%%%%%%%%%%%%% Construct sclck (hline-right, diagonal ne-sw,hline-right, diagonal se-nw) HMM  
% Construct the transmat (2,5,2,7)
transmat_sclck = blkdiag(transmat(:,:,2), transmat(:,:,5), transmat(:,:,2),transmat(:,:,7));
	% Update transmat at model transition
	for i=1:3 % As we have 3 transitions between 2 models
		transmat_sclck(i*Q,i*Q) = 0;
		transmat_sclck(i*Q,i*Q + 1) = 1;
	end

% Construct the obsmat (2,5,2)
obsmat_sclck = vertcat(obsmat(:,:,2), obsmat(:,:,5), obsmat(:,:,2), obsmat(:,:,7));
% Construct the prior
prior_sclck = zeros (1, 4*Q);
prior_sclck (1,1) = 1;

% Test sets Square, triangle, Z, vs 11 models ; 4 concat models + 7 primitive models
confusion_matrix = zeros(models_count);


% Testing Square, triangle and Z
% Print the number of samples
for j = 1 : models_count  % Square is @8, triangle @9, Z @10
	data = [acc_mapped_to_codebook{1,j}];
	size(data,2);
	for i=1:size(data,2)
		likelihood = zeros(1, models_count);
		
		% Against the primitive models 7 
		for k =1: primitives % 7 primitive models
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
				prior(:,:,k), transmat(:,:,k), obsmat(:,:,k));
		end

		k = primitives + 1;
		%%%% Against the concat models
		if k <= models_count 
			% Squarel
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_squarel, transmat_squarel, obsmat_squarel);
				k = k + 1;
		end

		if k <= models_count 
			% Squareu
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_squareu, transmat_squareu, obsmat_squareu);
			k = k + 1;
		end

		if k <= models_count 
			% triangle
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_triangle, transmat_triangle, obsmat_triangle);
			k = k + 1;
		end

		% Z
		if k <= models_count 
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_Z, transmat_Z, obsmat_Z);

			k = k + 1;
		end
		% sclck
		if k <= models_count 
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_sclck, transmat_sclck, obsmat_sclck);
			
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