# outputs.tf
# this will pring your public IP so you know where to look after the deployment

output "app_public_ip" {
  description = "Public IP address of the Streamlit EC2 instance."
  value       = aws_instance.app_server.public_ip
}

output "app_public_url" {
  description = "URL to access the Streamlit application."
  value       = "http://${aws_instance.app_server.public_ip}:8501"
}