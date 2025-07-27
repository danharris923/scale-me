"""
Shared utilities for the integrated site builder system.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


def setup_logging(level: int = logging.INFO) -> None:
    """Set up logging for the integrated system."""
    
    # Create logs directory
    logs_dir = Path("./logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"integration_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger for this module
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")


def validate_environment() -> bool:
    """Validate that all required environment variables are set."""
    
    required_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY", 
        "GCS_SERVER_URL"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logging.error(f"Missing required environment variables: {missing_vars}")
        logging.error("Please check your .env file or environment configuration.")
        return False
    
    # Validate optional but important vars
    optional_vars = ["VERCEL_TOKEN", "GCP_PROJECT_ID"]
    for var in optional_vars:
        if not os.getenv(var):
            logging.warning(f"Optional environment variable not set: {var}")
    
    logging.info("✅ Environment validation passed")
    return True


def create_project_structure(project_name: str, output_dir: str = "./generated") -> Path:
    """Create the directory structure for a generated project."""
    
    project_path = Path(output_dir) / project_name
    
    # Create main directories
    directories = [
        "pages",
        "pages/api", 
        "pages/category",
        "components",
        "styles",
        "public/images",
        "config",
        "lib",
        "hooks"
    ]
    
    for directory in directories:
        (project_path / directory).mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Created project structure at {project_path}")
    return project_path


def format_brand_name(brand_name: str) -> Dict[str, str]:
    """Format brand name for different uses."""
    
    # Create URL-friendly slug
    slug = brand_name.lower().replace(" ", "-").replace("_", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    
    # Create component-friendly name
    component_name = brand_name.replace(" ", "").replace("-", "").replace("_", "")
    
    # Create display name
    display_name = brand_name.title()
    
    return {
        "original": brand_name,
        "slug": slug,
        "component": component_name,
        "display": display_name,
        "filename": slug
    }


def generate_color_variations(primary_color: str) -> Dict[str, str]:
    """Generate color variations from a primary color."""
    
    # Simple color variations (in a real implementation, you'd use a color library)
    variations = {
        "primary": primary_color,
        "primary-dark": primary_color,  # Would be darkened
        "primary-light": primary_color,  # Would be lightened
        "primary-50": primary_color,     # 50% opacity
        "primary-25": primary_color      # 25% opacity
    }
    
    return variations


def validate_api_response(response_data: Dict[str, Any]) -> bool:
    """Validate that API response has the expected structure."""
    
    required_fields = ["count", "products"]
    
    for field in required_fields:
        if field not in response_data:
            logging.error(f"Missing required field in API response: {field}")
            return False
    
    if not isinstance(response_data["products"], list):
        logging.error("Products field is not a list")
        return False
    
    if response_data["count"] != len(response_data["products"]):
        logging.warning(f"Count mismatch: count={response_data['count']}, actual={len(response_data['products'])}")
    
    return True


def format_price(price: float) -> str:
    """Format price for display."""
    return f"${price:.2f}"


def truncate_text(text: str, max_length: int = 150) -> str:
    """Truncate text to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be filesystem-safe."""
    import re
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename


def get_template_path(template_name: str, template_type: str = "react") -> Path:
    """Get the path to a specific template file."""
    
    base_path = Path(__file__).parent.parent / "templates" / template_type
    template_file = base_path / f"{template_name}.template"
    
    if not template_file.exists():
        # Try without .template extension
        template_file = base_path / template_name
    
    return template_file


def load_template(template_path: Path) -> str:
    """Load template content from file."""
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def render_template(template_content: str, variables: Dict[str, Any]) -> str:
    """Render template with variables."""
    
    # Simple template rendering (replace {{variable}} with values)
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        if isinstance(value, (dict, list)):
            import json
            value = json.dumps(value, indent=2)
        template_content = template_content.replace(placeholder, str(value))
    
    return template_content


def save_file(content: str, file_path: Path) -> None:
    """Save content to file."""
    
    # Create directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logging.info(f"Saved file: {file_path}")


def copy_static_files(source_dir: Path, dest_dir: Path) -> None:
    """Copy static files from source to destination."""
    import shutil
    
    if source_dir.exists():
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        logging.info(f"Copied static files from {source_dir} to {dest_dir}")
    else:
        logging.warning(f"Source directory not found: {source_dir}")


def measure_performance(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logging.info(f"Function {func.__name__} took {duration:.2f} seconds")
        return result
    return wrapper