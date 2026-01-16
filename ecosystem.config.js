module.exports = {
  apps: [
    {
      name: "ModemAPI",
      script: "/home/wapa1274/Documents/ModemInterface/ModemApi.py",
      interpreter: "/home/wapa1274/Documents/ModemInterface/venv/bin/python",
      cwd: "/home/wapa1274/Documents/ModemInterface",

      autorestart: true,
      max_memory_restart: "500M",
      restart_delay: 3000,
      exp_backoff_restart_delay: 1000,

      instances: 1,
      exec_mode: "fork"
    },
    {
      name: "DoorContactAPI",
      script: "/home/wapa1274/Documents/DoorContactAPI/DoorContactAPI.py",
      interpreter: "/bin/python",
      cwd: "/home/wapa1274/Documents/DoorContactAPI",

      autorestart: true,
      max_memory_restart: "500M",
      restart_delay: 3000,
      exp_backoff_restart_delay: 1000,

      instances: 1,
      exec_mode: "fork"
    }
  ]
};
