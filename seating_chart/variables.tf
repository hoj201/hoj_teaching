# variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type to use."
  type        = string
  default     = "t2.micro" # Free-tier eligible
}

variable "ami_id" {
  description = "The AMI ID to use. This is a- Ubuntu 22.04 LTS for us-east-1."
  type        = string
  default     = "ami-053b0d53c279acc90"
  # Note: Find a current Ubuntu 22.04 AMI for your specific region if not using us-east-1.
}

variable "key_name" {
  description = "The name of your AWS EC2 Key Pair for SSH access."
  type        = string
  # IMPORTANT: You must create this key pair in the AWS console first.
  # Example: "my-aws-key"
}

variable "app_repo_url" {
  description = "The HTTPS URL of your Streamlit app's Git repository."
  type        = string
  # Example: "https://github.com/hoj201/hoj_teaching.git"
}

variable "app_entrypoint" {
  description = "The relative path to your main .py file from the repo root."
  type        = string
  default     = "streamlit.py" # e.g., "src/main_app.py"
}