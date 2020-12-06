resource "aws_alb" "airflow_alb" {
  name            = "${var.project_name}-${var.stage}-alb"
  subnets         = data.aws_subnet_ids.public.ids
  security_groups = [aws_security_group.application_load_balancer.id]
}

resource "aws_alb_target_group" "airflow_web_server" {
    name        = "${var.project_name}-${var.stage}-web-server"
    port        = 8080
    protocol    = "HTTP"
    vpc_id = data.aws_vpc.default.id
    target_type = "ip"

    health_check {
        interval = 10
        port = 8080
        protocol = "HTTP"
        path = "/health"
        timeout = 5
        healthy_threshold = 5
        unhealthy_threshold = 3
    }
}

# port exposed from the application load balancer
resource "aws_alb_listener" "airflow_web_server" {
    load_balancer_arn = aws_alb.airflow_alb.id
    port = "80"
    protocol = "HTTP"

    default_action {
        target_group_arn = aws_alb_target_group.airflow_web_server.id
        type = "forward"
    }
}
