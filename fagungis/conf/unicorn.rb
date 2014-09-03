# Set the working application directory
working_directory "%(rails_project_root)s"

# Unicorn PID file location
pid "%(unicorn_pids)s/unicorn.pid"

# Path to logs
# stderr_path "%(rails_user_home)s/logs/unicorn_%(project)s.log"
# stdout_path "%(rails_user_home)s/logs/unicorn_%(project)s.log"

# Unicorn socket
listen "/tmp/unicorn.%(project)s.sock"

# Number of processes
worker_processes %(unicorn_workers)s

# Time-out
timeout 60

before_fork do |server, worker|
  # Replace with MongoDB or whatever
  if defined?(ActiveRecord::Base)
    ActiveRecord::Base.connection.disconnect!
    Rails.logger.info('Disconnected from ActiveRecord -- Unicorn')
  end

  # # If you are using Redis but not Resque, change this
  # if defined?(Resque)
  #   Resque.redis.quit
  #   Rails.logger.info('Disconnected from Redis')
  # end

  sleep 1
end

after_fork do |server, worker|
  # Replace with MongoDB or whatever
  if defined?(ActiveRecord::Base)
    # config = Rails.application.config.database_configuration[Rails.env]
    # config['reaping_frequency'] = 10 # seconds
    # config['pool']            = 20
    ActiveRecord::Base.establish_connection
    Rails.logger.info('Connected to ActiveRecord -- Unicorn')
  end

  # # If you are using Redis but not Resque, change this
  # if defined?(Resque)
  #   Resque.redis = ENV['REDIS_URI']
  #   Rails.logger.info('Connected to Redis')
  # end
end
