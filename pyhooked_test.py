from pyhooked import Hook, KeyboardEvent


def handle_events(args):
    if isinstance(args, KeyboardEvent):
        if args.current_key == "B" and args.event_type == "key down":
            print("down B")

        if args.current_key == "B" and args.event_type == "key up":
            print("up B")

        if args.current_key == "A":
            hk.exit()


hk = Hook()
hk.handler = handle_events
hk.hook()
