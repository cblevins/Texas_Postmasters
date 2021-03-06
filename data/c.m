function c(C)

[m,n] = size(C);

count1 = 0;
count2 = 0;
avg1 = 0;
avg2 = 0;

for i = 1:m
    if C(i,1) == -1
        count1 = count1 + 1;
        avg1 = avg1 + C(i,2);
    else
        count2 = count2 + 1;
        avg2 = avg2 + C(i,2);
    end
end

count1
count2
avg1 = avg1 / count1
avg2 = avg2 / count2

maximum = max(C(:,1));
minimum = min(C(:,1));
unit = (maximum - minimum) / 50 + 1;
avg = zeros(50,1);
start = minimum + unit / 2;
for i = 1:50
    avg(i,1) = start + (i-1) * unit;
end

freq = zeros(50,1);
values = zeros(50,1);
for i = 1:size(C(:,1))
    for j = 1:50
        if C(i,1) < minimum + j * unit
            freq(j,1) = freq(j,1) + 1;
            values(j,1) = values(j,1) + C(i,2);
        end
    end
end
values = values ./ freq;
plot(avg, values)


end

