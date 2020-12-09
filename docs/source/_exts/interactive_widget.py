from sphinx.application import Sphinx
from docutils.parsers.rst import Directive
from docutils.nodes import raw


class IteractiveWidget(Directive):

    has_content = False
    required_arguments = 1
    _next_id = 0

    def run(self):
        IteractiveWidget._next_id += 1
        container_id = f"idom-widget-{IteractiveWidget._next_id}"
        view_id = self.arguments[0]
        return [
            raw(
                "",
                f"""
                <div>
                    <div id="{container_id}" class="interactive widget-container center-content" style="" />
                    <script async type="module">
                        const loc = window.location;
                        const idom_url = "//" + loc.host;
                        const http_proto = loc.protocol;
                        const ws_proto = http_proto === "https:" ? "wss:" : "ws:";

                        const mount = document.getElementById("{container_id}");
                        const enableWidgetButton = document.createElement("button");
                        enableWidgetButton.innerHTML = "Enable Widget";
                        enableWidgetButton.setAttribute("class", "enable-widget-button")

                        enableWidgetButton.addEventListener("click", () => {{
                            import("/client/src/layout.js").then((layout) => {{
                                fadeOutAndThen(enableWidgetButton, () => {{
                                    mount.removeChild(enableWidgetButton);
                                    mount.setAttribute("class", "interactive widget-container");
                                    layout.mountLayoutWithWebSocket(
                                      mount,
                                      ws_proto + idom_url + "/stream?view_id={view_id}"
                                    );
                                }});
                            }});
                        }});

                        function fadeOutAndThen(element, callback) {{
                            var op = 1;  // initial opacity
                            var timer = setInterval(function () {{
                                if ( op < 0.001 ) {{
                                    clearInterval(timer);
                                    element.style.display = "none";
                                    callback();
                                }}
                                element.style.opacity = op;
                                element.style.filter = 'alpha(opacity=' + op * 100 + ")";
                                op -= op * 0.5;
                            }}, 50);
                        }}

                        mount.appendChild(enableWidgetButton);
                    </script>
                </div>
                """,
                format="html",
            )
        ]


def setup(app: Sphinx) -> None:
    app.add_directive("interactive-widget", IteractiveWidget)
