provider "aws" {
  region = "eu-west-1"
}

resource "aws_instance" "jenkins3" {
  ami                    = "ami-2a7d75c0"
  instance_type          = "t2.large"
  iam_instance_profile   = "${aws_iam_instance_profile.jenkins.name}"
  key_name               = "${aws_key_pair.jenkins.key_name}"
  vpc_security_group_ids = ["${aws_security_group.jenkins_instance_security_group.id}"]

  tags {
    Name = "Jenkins3"
  }
}

resource "aws_eip" "jenkins3" {
  vpc = true
}

resource "aws_eip_association" "jenkins3_eip_assoc" {
  instance_id   = "${aws_instance.jenkins3.id}"
  allocation_id = "${aws_eip.jenkins3.id}"
}

resource "aws_key_pair" "jenkins" {
  key_name   = "${var.jenkins_public_key_name}"
  public_key = "${var.jenkins_public_key}"      # injected by Makefile-common
}

resource "aws_ebs_volume" "jenkins3_volume" {
  availability_zone = "${aws_instance.jenkins3.availability_zone}"
  type              = "gp2"
  size              = 100
}

resource "aws_volume_attachment" "jenkins3_ebs_att" {
  device_name = "/dev/xvdf"
  volume_id   = "${aws_ebs_volume.jenkins3_volume.id}"
  instance_id = "${aws_instance.jenkins3.id}"
}