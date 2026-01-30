module.exports = {
  apps: [
    {
      name: "nicopush",
      script: "src/cmd/nicopush.py",
      interpreter: "python",
      interpreter_args: "-u",
      cwd: __dirname,
      env: {
        PYTHONPATH: "src",
      },
      out_file: "logs/nicopush.log",
      error_file: "logs/nicopush.log",
      merge_logs: true,
      autorestart: true,
      max_restarts: 50,
      restart_delay: 5000,
      exp_backoff_restart_delay: 1000,
    },
    {
      name: "recorder",
      script: "src/cmd/recorder.py",
      interpreter: "python",
      interpreter_args: "-u",
      cwd: __dirname,
      env: {
        PYTHONPATH: "src",
      },
      out_file: "logs/recorder.log",
      error_file: "logs/recorder.log",
      merge_logs: true,
      autorestart: true,
      max_restarts: 50,
      restart_delay: 5000,
      exp_backoff_restart_delay: 1000,
    },
  ],
};
