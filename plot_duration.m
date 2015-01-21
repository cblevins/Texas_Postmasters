function plot_duration (D, pres)
    C = zeros(34942,1);
    for i = 1:34942
        val = -1;
        for j = 1:30
            if D(i,1) <= pres(j,1)
                val = j - 1;
                break
            end
        end
        C(i,1) = val;
    end
        
    M = zeros (30, 1);
    Counts = zeros(30,1);
    for i = 1:34942
        Counts(C(i,1)) = Counts(C(i,1)) + 1;
        M(C(i,1)) = M(C(i,1)) + D(i,2);
    end
    M = M ./ Counts;
    
    Vals = zeros(30,1);
    for i = 1:30
        Vals(i,1)=i;
    end
    %scatter(C(:,1), D(:, 2), 'b')
    %hold on
    scatter(Vals(:,1), M(:,1), 'r', 'filled')
    hold on
end