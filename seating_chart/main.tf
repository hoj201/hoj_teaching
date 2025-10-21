# main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. A new VPC for our app
resource "aws_vpc" "app_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "streamlit-vpc"
  }
}

# 2. A public subnet
resource "aws_subnet" "app_subnet" {
  vpc_id     = aws_vpc.app_vpc.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true # So we can access it from the internet
  availability_zone = "${var.aws_region}a"
  tags = {
    Name = "streamlit-subnet"
  }
}

# 3. An Internet Gateway to connect the VPC to the internet
resource "aws_internet_gateway" "app_igw" {
  vpc_id = aws_vpc.app_vpc.id
  tags = {
    Name = "streamlit-igw"
  }
}

# 4. A route table to route 0.0.0.0/0 to the IGW
resource "aws_route_table" "app_rt" {
  vpc_id = aws_vpc.app_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.app_igw.id
  }

  tags = {
    Name = "streamlit-rt"
  }
}

# 5. Associate the route table with our subnet
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.app_subnet.id
  route_table_id = aws_route_table.app_rt.id
}

# 6. Security Group to allow HTTP (8501) and SSH (22)
resource "aws_security_group" "streamlit_sg" {
  name        = "streamlit-sg"
  description = "Allow Streamlit (8501) and SSH (22) inbound"
  vpc_id      = aws_vpc.app_vpc.id

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Streamlit from anywhere"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # Allow all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "streamlit-sg"
  }
}

# 7. The EC2 Instance
resource "aws_instance" "app_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = aws_subnet.app_subnet.id
  vpc_security_group_ids = [aws_security_group.streamlit_sg.id]

  # This is the magic! We render the user_data.sh script as a template,
  # passing in our variables so the script knows what to download and run.
  user_data = templatefile("${path.module}/user_data.sh", {
    app_repo_url   = var.app_repo_url
    app_entrypoint = var.app_entrypoint
  })

  tags = {
    Name = "StreamlitAppServer"
  }
}