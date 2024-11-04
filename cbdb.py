import toml
import matplotlib.pyplot as plt

class Experiment:
    def __init__(self, name, authors, year, beta, beta_sigma, beta_sys, arxiv, doi):
        self.name = name
        self.authors = authors
        self.year = year
        self.beta = beta
        self.beta_sigma = beta_sigma
        self.beta_sys = beta_sys
        self.arxiv = arxiv
        self.doi = doi

    def __repr__(self):
        return (f"Experiment(name={self.name}, authors={self.authors}, year={self.year}, "
                f"beta={self.beta}, beta_sigma={self.beta_sigma}, beta_sys={self.beta_sys}, "
                f"arxiv={self.arxiv}, doi={self.doi})")

class ExperimentCollection:
    def __init__(self, file_path):
        self.experiments = self.load_experiments(file_path)
        
    def load_experiments(self, file_path):
        data = toml.load(file_path)
        experiments = []
        for key in data:
            for exp_data in data[key]:  # Loop through each dictionary in the list
                experiment = Experiment(
                    name=exp_data["name"],
                    authors=exp_data["authors"],
                    year=exp_data["year"],
                    beta=exp_data["beta"],
                    beta_sigma=exp_data["beta_sigma"],
                    beta_sys=exp_data["beta_sys"],
                    arxiv=exp_data["arxiv"],
                    doi=exp_data["doi"]
                )
                experiments.append(experiment)
        return experiments
    
    def __iter__(self):
        return iter(self.experiments)

    def __repr__(self):
        return "\n".join([str(exp) for exp in self.experiments])
    
    def plot_beta_with_error(self):
        # Sort experiments by year
        sorted_experiments = sorted(self.experiments, key=lambda x: x.year)

        # Extract data for plotting
        names = [exp.name for exp in sorted_experiments]
        years = [exp.year for exp in sorted_experiments]
        betas = [exp.beta for exp in sorted_experiments]
        beta_sigmas = [exp.beta_sigma for exp in sorted_experiments]

        # Plot beta with error bars
        plt.figure(figsize=(10, 6))
        plt.errorbar(range(len(betas)), betas, yerr=beta_sigmas, fmt='o', capsize=5)
        plt.axhline(0.3, color='r', linestyle='--', label='$\\beta = 0.3$')
        plt.xticks(range(len(names)), names, rotation=45, ha="right")
        plt.xlabel("Experiments")
        plt.ylabel("Beta")
        plt.tight_layout()
        plt.legend()