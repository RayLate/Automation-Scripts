class GitHub {
    constructor() {
        this.client_id = '984d54da692094d70ea0';
        this.client_secret = 'c8f9254846ba5393af59e767e03e7f413e8b4274';
        this.repos_count = 5;
        this.repos_sort = 'created: asc'
    };
    async getUser(user) {
        const profileResponse = await fetch(`https://api.github.com/users/${user}?client_id=${this.client_id}&client_secret=${this.client_secret}`);
        const reposResponse = await fetch(`https://api.github.com/users/${user}/repos?per_page=${this.repos_count}&sort=${this.repos_sort}&client_id=${this.client_id}&client_secret=${this.client_secret}`);

        const profile = await profileResponse.json();
        const repos = await reposResponse.json();

        return {
          profile,
          repos
        };
      };

};
