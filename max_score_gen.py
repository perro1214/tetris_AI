#import pprint

argv = input()

with open('score.csv', 'r') as file:
    Y = []
    for i,line in enumerate(file):
        if i%5 == 0:
            Y.append([line.strip().split(',')[0],float(line.strip().split(',')[1])])
        else:
            Y[i//5][1] += float(line.strip().split(',')[1])
Y = list(map(lambda x: [x[0],x[1]/5], Y))
result = Y[-1][0].replace("model_gen/gen_", "").replace(".keras", "").replace(" ","")
Y = sorted(Y, key=lambda x: x[1], reverse=True)
#pprint.pprint(Y)
result2 = Y[0][0].replace("model_gen/gen_", "").replace(".keras", "").replace(" ","")

print(result2,argv,result)