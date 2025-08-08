import json
import os

class DataManager:
    
    DEFAULT_DATA = {
        
        "COOKIES": "c_user=...;fr=...;sb=...;xs=...;datr=...",
        
        "GUI_HOAT_DONG": {
            "links": [
                "https://www.facebook.com/profile.php?id=...",
                "https://m.facebook.com/...",
                "https://www.facebook.com/..."
            ],
            "message": \
'''[VIT][ĐI DẠY]
- Thời gian: ...
- Địa điểm: Nhà nuôi dưỡng trẻ em Hữu Nghị Đống Đa (102 phố Yên Lãng, quận Đống Đa)
- Số lượng: 6 - 8 TNV
- Trang phục: Áo xanh, đeo thẻ SV
CF ĐĂNG KÝ KÈM PHƯƠNG TIỆN (NẾU CÓ).
HẠN ĐĂNG KÝ: ...'''
        },
        
        "TAG_THANH_VIEN": {
            "link_post": "https://www.facebook.com/groups/.../posts/...",
            "link_group": "https://www.facebook.com/groups/...",
            "members": ["Văn A", "Thị B", "Nguyễn C"],
            "comment": "cf nào mọi người",
            "delay": None
        }
    }
    
    def __init__(self, data_folder: str, data_path: str):
        self.folder_path = data_folder
        self.data_path = data_path
        self.auto_save = True
        self.error_link = ""
        self._ensure_data_directory()
        
        if not os.path.exists(self.data_path): # Nếu chưa có file data -> Tạo (kèm luôn sheet Login)
            self.save_data()
            
    def load_data(self) -> None:
        """Load data from JSON file or create with defaults if not exists"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = self.DEFAULT_DATA
    
    def save_data(self) -> bool:
        """Save configuration to JSON file"""
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except:
            return False
        return True
    
    def set_autosave(self):
        self.auto_save = not self.auto_save

    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            
    def clear_data(self) -> None:
        """Clear all stored data"""
        if os.path.exists(self.data_path):
            os.remove(self.data_path)
        if os.path.exists(self.data_path):
            os.remove(self.data_path)