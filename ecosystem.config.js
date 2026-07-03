module.exports = {
  apps: [{
    name: 'octopus-watch',
    script: 'octopus_agent.py',
    interpreter: '/home/eliot/octopus-agent/venv/bin/python3',
    args: '--watch',
    cwd: '/home/eliot/octopus-agent',
    env: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY
    }
  }]
}
