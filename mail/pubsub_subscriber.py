from google.cloud import pubsub_v1

PROJECT_ID = "gmail-tracking-491020"
SUBSCRIPTION_ID = "Incoming-emails-sub"


def callback(message):
    """Called when a message is received."""
    print(f"Received message: {message.data.decode('utf-8')}")

    

    message.ack()


def start_subscriber():
    """Start listening for messages."""
    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

        print(f"Listening for messages on {subscription_path}...")

        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
            print("Subscriber stopped.")


if __name__ == "__main__":
    start_subscriber()
