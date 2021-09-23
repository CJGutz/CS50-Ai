import os
from random import choices, sample
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}") 
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}") 


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) #- {filename} # removing filename leaves set of links from recursion empty

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    print(pages)
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    probabilities = {}
    
    # if page has no links, remove damping_factor    
    damping_factor = 0 if len(corpus[page]) == 0 else damping_factor
    
    # probability of chosen by complete random
    for random_page in corpus.keys():
        probabilities[random_page] = round((1-damping_factor)/len(corpus), 5)
    
    # probability of chosen by link
    for linked_page in list(corpus[page]):
        probabilities[linked_page] += damping_factor/len(corpus[page])
        
        
    return probabilities
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # make dictionary page_rank
    page_rank = {}
    for page in corpus.keys():
        page_rank[page] = 0
        
    # pick and visit first page
    next_page = sample(corpus.keys(), k = 1)[0]
    
    # try n transitions
    for i in range(n):
        
        # add visit to current page
        page_rank[next_page] += 1

        # get the transition model for current page
        pages = transition_model(corpus, next_page, damping_factor)
        
        # list of probabilites
        probabilities = []
        for page in pages:
            probabilities.append(round(pages[page] * 100))
            
        # choose a random page
        next_page = choices(list(pages), probabilities, k = 1)[0]
        

        
    # divide each page_rank number by n samples
    for page in list(page_rank):
        page_rank[page] /= n
        
    return page_rank
        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    
    # make dictionary page_rank and add 1 / N to each page
    page_rank = {}
    for page in corpus.keys():
        page_rank[page] = (1) / len(corpus)
        
        
    # dictionary of links to each page
    inv_corpus = {}
    for page in corpus.keys():
        links = []
        for count, value in enumerate(corpus.values()):
            for i in value:
                if i == page:
                    links.append(list(corpus.keys())[count])
        inv_corpus[page] = links
            
        
    # add sum of links to each page
    pr_change = 1
    while pr_change > 0.001: # iterate until small change
        pr_change_list  = []
        
        for page in corpus.keys():
            
            # find the sum of each link: PR(i) over NumLinks(i)
            sum_i = 0
            for link in inv_corpus[page]: 
                sum_i += page_rank[link] / len(corpus[link])
            sum_i *= damping_factor
            
            # find change and set new page_rank
            new_pr = (1-damping_factor) / len(corpus) + sum_i
            pr_change_list.append(abs(page_rank[page] - new_pr))
            page_rank[page] = new_pr
            
        pr_change = max(pr_change_list)
   
    return page_rank


if __name__ == "__main__":
    main()
