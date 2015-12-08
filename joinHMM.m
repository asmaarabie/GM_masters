function [s_transmat, s_obsmat, s_initmat] = joinHMM (transmat,obsmat,initmat,levels)
	
	method = 2;
	% S_ --> Super
	Q = size(transmat,1);
	O = size(obsmat,2);
	count = size(levels,2);
		
	if method == 1
		s_Q = count*(Q-1)+1;
		s_transmat = zeros (s_Q);
		s_obsmat = zeros (s_Q, O);
		s_initmat = zeros (1,s_Q);

		% Concatenate transmission matrices
		si = 1;
		for i = 1:count
			ei= si + Q - 1;
			dec = not (i== count); % if this is not the last level remove the last record from transmat
			s_transmat(si:ei, si:ei) = transmat(:,:, levels(i));
			s_obsmat (si:ei ,:) = obsmat(:,:, levels(i));
			si = ei;
		end

		% Construct init matrix
		s_initmat(1, 1:Q) = initmat(:,:,1);
	end
	if method == 2
		s_transmat = zeros (count*Q);
		s_obsmat = zeros (count*Q, O);
		s_initmat = zeros (1,count*Q);

		si = 1;
		
		for i = 1:count
			ei= si + Q - 1;
			s_transmat(si:ei, si:ei) = transmat(:,:, levels(i));
			if not (i== count)
				s_transmat(i*Q,i*Q) = 0.5;
				s_transmat(i*Q,i*Q + 1) = 0.5;
			end
			s_obsmat (si:ei ,:) = obsmat(:,:, levels(i));
			si = ei+1;
		end
		
		s_initmat (1, 1:Q) = initmat(:,:,1);
	end

end