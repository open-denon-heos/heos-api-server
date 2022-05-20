from flask import Flask, request, render_template, Response

from heospy import *

app = Flask(__name__)
app.debug = True


def _setup(rediscover):
    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
        # initialize connection to HEOS player
        try:
            p = HeosPlayer(rediscover=rediscover, config_file="config/config.json")
            logging.info(p)
        except HeosPlayerConfigException:
            logging.info("Try to find a valid config file")
            raise
        except HeosPlayerGeneralException:
            # if the connection failed, it might be because the cached IP for
            # the HEOS player is not valid anymore. We check if we can rediscover
            # the new IP of the HEOS player
            logging.info("First connection failed. Try to rediscover the HEOS players.")
            p = HeosPlayer(rediscover=True, config_file="config/config.json")
        except:
            logging.error("Someting unexpected got wrong...")
            raise

    except:
        raise

    return p


@app.before_first_request
def setup():
    p = _setup(False)
    logging.info(p.status())


@app.route("/status")
def status():
    p = _setup(False)
    return Response(json.dumps(p.status(), indent=2), mimetype='application/json')


@app.route("/<cmd>/<subcmd>")
def execute(cmd, subcmd):
    p = _setup(False)

    args = {}
    for key, value in request.args.items():
        args[key] = value

    all_results = p.cmd(f"{cmd}/{subcmd}", args)
    return Response(json.dumps(all_results, indent=2), mimetype='application/json')


@app.route("/")
def sample():
    return render_template("index.html")


'''
Turn on and off the AVR we need to go via legacy API
https://assets.denon.com/DocumentMaster/us/AVR1713_AVR1613_PROTOCOL_V8%206%200%20(2).pdf
'''


@app.route("/on")
def power_on():
    p = _setup(False)

    telnet = telnetlib.Telnet(p.host, 23, timeout=TIMEOUT)
    command = "PWON"
    telnet.write(command.encode('ascii') + b'\n')
    all_results = p.cmd(f"player/get_play_state", {})
    return Response(json.dumps(all_results, indent=2), mimetype='application/json')


@app.route("/off")
def power_off():
    p = _setup(False)
    # https: // assets.denon.com / DocumentMaster / us / AVR1713_AVR1613_PROTOCOL_V8 % 206 % 200 % 20(2).pdf
    telnet = telnetlib.Telnet(p.host, 23, timeout=TIMEOUT)
    command = "PWSTANDBY"
    telnet.write(command.encode('ascii') + b'\n')
    all_results = p.cmd(f"player/get_play_state", {})
    return Response(json.dumps(all_results, indent=2), mimetype='application/json')
