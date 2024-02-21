from src.core.utils.dynamic_router import search_routers, get_current_directory

package_path = get_current_directory(__file__)

router_urls = search_routers(package_path)
