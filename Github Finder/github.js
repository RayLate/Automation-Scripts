class GitHub {
    constructor() {
        this.client_id = '984d54da692094d70ea0';
        this.client_secret = 'c8f9254846ba5393af59e767e03e7f413e8b4274';
    };
    async getUser(user) {
        const profileResponse = await fetch(`https://api.github.com/users/${user}?client_id=${this.client_id}&client_secret=${this.client_secret}`);

        const profile = await profileResponse.json();

        return {
          profile
        }
      }
};
