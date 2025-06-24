# Use a Kali Linux base image for attack tools
# Kali has many security tools pre-installed
FROM kalilinux/kali-rolling  

# Install hping3 for SYN flood attacks
# Install hping3 and clean up
RUN apt-get update && apt-get install -y hping3 && rm -rf /var/lib/apt/lists/*  

# Copy the attack script into the container
# Add attack script
COPY attack.sh /attack.sh  

# Make the script executable
# Ensure script can be run
RUN chmod +x /attack.sh  

# Default command to run the attack script (overridden by docker-compose)
CMD ["/attack.sh"]  # By default, run the attack script