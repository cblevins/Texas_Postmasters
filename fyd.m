function fyd (FY)
    Vals = [0,1,2,3,4];
    Counts = zeros(5, 1);
    Means = zeros(5,1);
    
    for i = 1:34942
        Counts(FY(i,1) + 1) = Counts(FY(i,1) + 1) + 1;
        Means(FY(i,1) + 1) = Means(FY(i,1) + 1) + FY(i,2);
    end
    
    Means = Means ./ Counts;

    %scatter(FY(:,1), FY(:,2), 'b')
    %hold on
    scatter(Vals, Means(:,1), 'r', 'filled')
end