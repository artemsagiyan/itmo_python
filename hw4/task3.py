import multiprocessing
import time
import codecs

def rot13(text):
    return codecs.encode(text, 'rot13')

def process_a(queue_in, queue_out):
    while True:
        try:
            msg = queue_in.get()
            lower_msg = msg.lower()
            time.sleep(5)
            queue_out.put(lower_msg)
        except Exception as e:
            print(f"Process A error: {e}")
            break


def process_b(queue_in, queue_out_main):
    while True:
        try:
            msg = queue_in.get()
            rot13_msg = rot13(msg)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Process B received: {msg}, Rot13: {rot13_msg}")
            queue_out_main.put(rot13_msg)
        except Exception as e:
            print(f"Process B error: {e}")
            break


def main():
    queue_a_in = multiprocessing.Queue()
    queue_ab = multiprocessing.Queue()
    queue_main = multiprocessing.Queue()

    process_a_instance = multiprocessing.Process(target=process_a, args=(queue_a_in, queue_ab))
    process_b_instance = multiprocessing.Process(target=process_b, args=(queue_ab, queue_main))

    process_a_instance.start()
    process_b_instance.start()

    with open("artifacts/results_task3.txt", "w") as log_file:
        try:
            while True:
                input_message = input("Enter message (or 'quit' to exit): ")
                if input_message.lower() == 'quit':
                    break
                
                log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Main process sent: {input_message}\n")
                queue_a_in.put(input_message)

                #Получаем результат из очереди B
                if not queue_main.empty():
                    rot13_result = queue_main.get()
                    log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Main process received from B: {rot13_result}\n")


        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            process_a_instance.join()
            process_b_instance.join()
            print("Processes terminated.")

if __name__ == "__main__":
    main()

