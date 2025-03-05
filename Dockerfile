# Use the Nginx image
FROM nginx:latest  

# Copy your website files to the default Nginx HTML directory
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
