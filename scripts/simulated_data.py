# Program used to crete simulated Rainbow Trout genomic data.
# No parser implemented - data prameters specified inside the code.
# Coded by @ndre! RATM
# Should you have any questions: andeeri@protonmail.com / https://github.com/andeeri-k
##########################################################

######## Import packages #######
import random
################################


# Population size and proportion.
population_size = random.randint(10000, 15000)  # total population size
males = 40                                      # percentage of males, females = 100% - males


males = males * 0.01   # convert to [0, 1] scale
females = 1 - males    # females

# Create vector of sex
n_males = int(population_size * males)  # calculate number of males in requested population
n_females = int(population_size * females)  # calculate number of females in requested population
fish_sex = [0 for i in range(n_males)] + [1 for j in range(n_females)]  # create vector of sex records
random.shuffle(fish_sex)  # sample shuffle

# Print some data check
if population_size != len(fish_sex):
    print(f"Warning! Created population is smaller than requested.")
    print(f"Number of samples is {len(fish_sex)}")
    print(f"Number of males: {fish_sex.count(0)}; females: {fish_sex.count(1)}")
    print(f"Usually no actions needed. Size - percentage are not aliquot.")
else:
    print(f"Number of samples is {len(fish_sex)}")
    print(f"Number of males: {fish_sex.count(0)}; females: {fish_sex.count(1)}")


# Function to create marker data
# From Palti et al. (2015) whe assume that males are biased towards heterozygote (i.e. 1)
def marker_vector(sex_vector: list, error_rate: int, missing_rate: int):
    """Function to create single marker vectour with desired missing and error rates
     
    Args:  
       sex_vector = list of sex observations ie [0,1,0,1...]
       error_rate = integer [0,100] number of erronius SNPs
       missing_rate = integer [0, 100] number of missing SNPs 
    
    Returns:
        list: snp_vectour.    
    """
    snp_vector = []
    error_rate *= 0.01
    missing_rate *= 0.01

    # Create initial true genomic vector based on sex information provided
    for value in sex_vector:
        if value == 0:
            snp_vector.append(1)
        elif value == 1:
            snp_vector.append(2)

    # Randomly re-code desired number of samples as missing and mismatch
    missing_snps = int(missing_rate * len(sex_vector)) # number of samples with missing SNPs
    error_snps = int(error_rate * (len(sex_vector)-missing_snps)) # number of samples with wrong SNPs
    change_snp = random.sample(range(0, len(snp_vector) - 1), missing_snps+error_snps) # index of samples for re-code
    n_round = 1

    for sample in change_snp:
        if n_round <= missing_snps:
            snp_vector[sample] = 5
            n_round += 1
        else:
            snp_vector[sample] = 2 if snp_vector[sample] == 1 else 1
            n_round += 1

    return snp_vector


# Function to save the data
def save_my_data(data: dict, file_name: str):
    """ Function to save the data 
       
    Args:
       data = dictionary with sex and marker values
       file_name = string, name of output file
    
    Returns:
        Always returns None.  
    """
    with open(file_name, 'w') as running_file:
        for i in range(len(data['sex'])):
            running_file.write(f"{','.join(str(data[key][i]) for key in data)}\n")
    return None


# Creating data
## Data set 1: 15 markers, missing rate = 5%, error rate = 5%
sim_5 = {'sex': fish_sex} # initial data
for i in range(1, 16):
    sim_5[f"M_{i}"] = marker_vector(sim_5['sex'], error_rate=5, missing_rate=5)
save_my_data(sim_5, 'sim_5.dat') # save the data

## Data set 2: 15 markers, missing rate = 5%, error rate = 50%
sim_50 = {'sex': fish_sex} # initial data
for i in range(1, 16):
    sim_50[f"M_{i}"] = marker_vector(sim_50['sex'], error_rate=50, missing_rate=5)
save_my_data(sim_50, 'sim_50.dat') # save the data

## Data set 3: 15 markers, missing rate = 5%, error rate = random from 5 to 50%
sim_rand = {'sex': fish_sex} # initial data
random_error_rate = random.sample(range(5, 50), 15) # vectour of random error rates
for i in range(1, 16):
    sim_rand[f"M_{i}"] = marker_vector(sim_rand['sex'], error_rate=random_error_rate[i-1], missing_rate=5)
save_my_data(sim_rand, 'sim_rand.dat') # save the data

## Data set 4: missing rate = 5%, 5 markers error rate = random 5 to 10%, 10 markers error rate = random 20 to 60 %
sim_real = {'sex': fish_sex} # initial data
### SNP 1-5
random_error_rate = random.sample(range(5, 10), 5) # vectour of random error rates
for i in range(1, 6):
    sim_real[f"M_{i}"] = marker_vector(sim_real['sex'], error_rate=random_error_rate[i-1], missing_rate=5)
random_error_rate = random.sample(range(20, 60), 10) # vectour of random error rates
### SNP 6-15
for i in range(6, 16):
    sim_real[f"M_{i}"] = marker_vector(sim_real['sex'], error_rate=random_error_rate[i-6], missing_rate=5)
save_my_data(sim_real, 'sim_real.dat') # save the data
