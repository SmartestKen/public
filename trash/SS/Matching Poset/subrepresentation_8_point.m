clear all; clc
format compact
A8 = load('subrepresentation[8].txt');
A62 = load('subrepresentation[6, 2].txt');
A44 = load('subrepresentation[4, 4].txt');
A422 = load('subrepresentation[4, 2, 2].txt');
A2222 = load('subrepresentation[2, 2, 2, 2].txt');
A = {A8, A62, A44,A422,A2222};
combos = cell(4,0);
combos{1} = nchoosek(1:5,1);
combos{2} = nchoosek(1:5,2);
combos{3} = nchoosek(1:5,3);
combos{4} = nchoosek(1:5,4);
counter = 0;

pivots = cell(30,0);
for i = 1:4
    for j = 1:size(combos{i})
        counter = counter + 1;
        chosenIdx = combos{i}(j,:);
        
        %disp(chosenIdx)
        subMat = A{chosenIdx(1)};
        for k = 2:size(chosenIdx,2)
            subMat = [subMat; A{chosenIdx(k)}];
        end
        % disp(all(subMat == [A8; A44;A422;A2222],'all'))

        disp(rank(null(subMat)'))
        disp(size(null(subMat)'))
        [temp,pivot] = rref(fliplr(null(subMat)'));
        pivots{counter} = 106 - pivot;
        %disp(pivot)
        %disp('--------------')
        
    end
end


relationMat = ones(105,105);
relationMat = triu(relationMat,1);
for i = 1:105
    for j = i+1:105
        for k = 1:30
            temp = ismember([i,j], pivots{k});
            %disp(temp)
            if ~all(temp) && any(temp)
                relationMat(i,j) = 0;
                break;
            end
        end
    end
end


% first way to get inequi component
temp = 1:105;

for i = 1:105
    for j = i+1:105
        if (relationMat(i,j) == 1) && (temp(i) ~= 0) && (temp(j) ~= 0)
            % both in temp, remove largest

            temp(j) = 0;
 
        end
    end
end



% second way to get inequi component (for verification)
minequi = 1:105;
for i = 1:105
    for j = i+1:105
        if relationMat(i,j) == 1 
            minequi(j) = minequi(i);
        end
    end
end
minequi = unique(minequi);
for i = 1:size(minequi,2)
    for j = i+1:size(minequi,2)
        if relationMat(minequi(i),minequi(j)) == 1 
            disp("error")
        end
    end
end



% check if all inequivalent
temp2 = nonzeros(temp)';
for i = 1:size(temp2)
    for j = i+1:size(temp2)
        if relationMat(temp2(i), temp2(j)) == 1
            disp([temp2(i), temp2(j)])
        end
    end
end

%%
for i=1:30
    disp(size(pivots{i},2))
end







            
                


        
        