resource "aws_s3_bucket" "bucket_publico" {
  bucket = "meu-bucket-inseguro"
  acl    = "public-read"
}

resource "aws_security_group" "sg_inseguro" {
  name = "sg_inseguro"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}