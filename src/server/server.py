from concurrent import futures

import grpc
import logging

from src.generated import question_pb2_grpc
from src.server.services.question_service import QuestionService


def serve():
    """gRPC 서버 시작"""
    # 서버 설정
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 서비스 등록
    question_pb2_grpc.add_QuestionServiceServicer_to_server(
        QuestionService(), server
    )

    # 포트 설정
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)

    # 서버 시작
    server.start()
    print(f"gRPC 서버가 {listen_addr}에서 시작되었습니다.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
        server.stop(0)


if __name__ == '__main__':
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 서버 실행
    serve()