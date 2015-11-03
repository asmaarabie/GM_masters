load('Datasets/processed/acc_readings.mat');



gestures = size(acc_readings,2);
ratehz = 60;
for j = 1 : gestures
	gesture = [acc_readings{1,j}];
	files = size(gesture,2);
	for g=1: files
		file = gesture{1,g};
		velocity=(cumtrapz(file(:,:))/ratehz);
		disp=(cumtrapz(velocity)/ratehz);

		acc_readings{1,j}{1,g} = disp;
	end
end

save('Datasets/processed/acc_readings_dist.mat','acc_readings');