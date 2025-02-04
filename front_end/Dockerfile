# Use Nginx as the base image
FROM nginx:alpine

# Remove default Nginx website files
RUN rm -rf /usr/share/nginx/html/*

# Copy your static frontend files to Nginx's serving directory
COPY *.html /usr/share/nginx/html
COPY js/ usr/share/nginx/js/
# Copy a custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for serving the website
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
