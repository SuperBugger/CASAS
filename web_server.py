from flask import Flask, jsonify, request
from flask_cors import CORS
from core import PluginManager

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


plugin_manager = PluginManager()
plugin_manager.load_plugins()


@app.route('/api/plugins', methods=['GET'])
def list_plugins():
    plugins = list(plugin_manager.plugins.keys())
    return jsonify(plugins)


@app.route('/api/plugin/<szi_name>/<command>', methods=['GET'])
def run_plugin_command(szi_name, command):
    output_json = request.args.get('json', 'false').lower() == 'true'
    directory = request.args.get('directory', '')

    try:
        if szi_name == 'integrity_check' and command == 'status' and directory:
            result = plugin_manager.run_plugin(szi_name, command, output_json, directory=directory)
        else:
            result = plugin_manager.run_plugin(szi_name, command, output_json)

        if result is None:
            raise ValueError(f"No such SZI: {szi_name}")

        if output_json:
            return jsonify(result)
        else:
            return result
    except Exception as e:
        app.logger.error(f"Error running plugin {szi_name} with command {command}: {e}")
        return jsonify({'error': str(e)}), 500
