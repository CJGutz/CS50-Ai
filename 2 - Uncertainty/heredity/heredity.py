import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    

    joint_probability = 1
    
    for person in people.keys():
        
        
        gene = 1 if person in one_gene else 2
        gene = 0 if person not in one_gene and person not in two_genes else gene
        trait = True if person in have_trait else False
        
        mother = people[person]["mother"]
        father = people[person]["father"]
        

        if mother is not None and  father is not None:
            
            mother_gene = (1 if mother in one_gene else
                           2 if mother in two_genes else 0)
            
            father_gene = (1 if mother in one_gene else
                           2 if mother in two_genes else 0)
            
            
            # dictionary where first keys are nr of parents genes and second keys are which how many genes are inherited to child
            factors = {
                0 : {
                    0 : 1 - PROBS["mutation"], # P(fra null til null)
                    1 : PROBS["mutation"] # P(fra 0 til en)                
                },
                1 : {
                    0 : 1 / 2, # P(fra en til null og ikke mutasjon) + P(fra 1 til 1 og mutasjon )
                    1 : 1 / 2 # P(fra en til en og ikke mutasjon) + P(fra en til null og mutasjon)
                 },
                2 : {
                    0 : PROBS["mutation"], # P(fra to til null)
                    1 : (1 - PROBS["mutation"]) # P(fra to til 1)
                }
            }
            
            # 3 different algorithms for calculating child getting 0, 1 or 2 genes
            alg = {
                0 : [[0,0]], # P(-M, -F)
                1 : [[1,0], [0,1]], # P(M, -F) + P(-M, F)
                2 : [[1,1]] # P(M, F)
            }
            
            sum_prob = 0
            for i in alg[gene]:

                m_factor = factors[mother_gene][i[0]]
                f_factor = factors[father_gene][i[1]]
     
            joint_probability *= PROBS["trait"][gene][trait] * (m_factor * f_factor)  
            
        else:
            joint_probability *= PROBS["gene"][gene] * PROBS["trait"][gene][trait]
            
    return joint_probability
     
    
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    for person in probabilities.keys():
        
        gene = 1 if person in one_gene else 2
        gene = 0 if person not in one_gene and person not in two_genes else gene
        trait = True if person in have_trait else False
        
        
        probabilities[person]["gene"][gene] += p
        probabilities[person]["trait"][trait] += p
        


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities.keys():
        
        sum_genes = 0
        for gene in probabilities[person]["gene"].values():
            sum_genes += gene
        factor = 1 / sum_genes
        for gene in probabilities[person]["gene"].keys():
            probabilities[person]["gene"][gene] *= factor
            
        
        sum_traits = 0
        for trait in probabilities[person]["trait"].values():
            sum_traits += trait
        factor = 1 / sum_traits
        for trait in probabilities[person]["trait"].keys():
            probabilities[person]["trait"][trait] *= factor
            
    
        
    
if __name__ == "__main__":
    main()
