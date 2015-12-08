% TODO: run python here
%commandStr = 'python /Users/myName/pathToScript/sqr.py 2';
% [status, commandOut] = system(commandStr);
% if status==0
%     fprintf('squared result is %d\n',str2num(commandOut));
% end
clc;
clear;
addpath(genpath('~/HMMall'));
load('Datasets/processed/line60hz_train.mat');
load('Datasets/processed/line60hz_test.mat');

primitives = size(train,2);

% Prepare HMM
Q = 8; 
O = 8;
max_iter =10;

% initial guess of parameters
prior1 = zeros(Q,1);
prior1 (1:Q) = 1/Q;
transmat1 = zeros(Q, Q);
for i = 1:(Q-1)
    transmat1(i,i) = 0.5;
    transmat1(i,i+1) = 0.5;
end
transmat1(Q, Q) = 1;
obsmat1 = ones(Q, O)* (1/O); 

transmat= zeros (Q, Q,size(train,2));
obsmat  = zeros(Q, O,size(train,2));
LL 		= zeros (1, max_iter, size(train,2));
prior	= zeros (Q,1, size(train,2));

% Train primitive models
for i=1:size(train,2)
	[LL, prior(:,1,i), transmat(:,:,i), obsmat(:,:,i)] = dhmm_em(train{1,i,:}, prior1, transmat1, obsmat1, 'max_iter', max_iter);
end

%%%%%%%%%%%%% Concatenated models
%TODO: right them in a jagged array

% Construct square l-d-r-u HMM (1,3,2,4)
[transmat_squarel, obsmat_squarel, prior_squarel] = joinHMM (transmat,obsmat,prior,[1 3 2 4]);

% Construct square r-d-l-u HMM (2,3,1,4)
[transmat_squarer, obsmat_squarer, prior_squarer] = joinHMM (transmat,obsmat,prior,[2 3 1 4]);

% Construct trianglecw dline-nw-se, hline-left, dline-sw-ne HMM (6,1,8)
[transmat_trianglecw, obsmat_trianglecw, prior_trianglecw] = joinHMM (transmat,obsmat,prior,[6 1 8]);

% Construct triangle ccw dline-ne-sw, hline-right, dline-se-nw HMM  (5,2,7)
[transmat_triangleccw, obsmat_triangleccw, prior_triangleccw] = joinHMM (transmat,obsmat,prior,[5 2 7]);

% Construct Z (hline-right, diagonal ne-sw,hline-right) HMM  (2,5,2)
[transmat_Z, obsmat_Z, prior_Z] = joinHMM (transmat,obsmat,prior,[2 5 2]);

% Construct tick (dline-nw-se, dline-sw-ne) HMM (6,8)
[transmat_tick, obsmat_tick, prior_tick] = joinHMM (transmat,obsmat,prior,[6 8]);

%test = test(1:8)
% Test sets Square, triangle, Z, vs 11 models ; 4 concat models + 7 primitive models
confusion_matrix = zeros(size(test,2));


% Testing Square, triangle and Z
% Print the number of samples
accuracy_count = 0;
class_count = zeros (1,size(test,2));
for j = 1 : size(test,2)  % Square is @8, triangle @9, Z @10
	data = [test{1,j}];
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
		if k <= size(test,2) 
			% Squarel
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_squarel, transmat_squarel, obsmat_squarel);
				k = k + 1;
		end

		if k <= size(test,2)
			% Squarer
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_squarer, transmat_squarer, obsmat_squarer);
			k = k + 1;
		end

		if k <= size(test,2)
			% trianglecw
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_trianglecw, transmat_trianglecw, obsmat_trianglecw);
			k = k + 1;
		end

		if k <= size(test,2)
			% triangleccw
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_triangleccw, transmat_triangleccw, obsmat_triangleccw);
			k = k + 1;
		end
		
		if k <= size(test,2) 
			% Z
			likelihood(:,k) = dhmm_logprob(data{1,i}, ...
					prior_Z, transmat_Z, obsmat_Z);

			k = k + 1;
		end
		
		if k <= size(test,2) 
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
Accuracy_vs_class_count =  sum(diag(confusion_matrix)./class_count')/size(confusion_matrix,1)

