import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import { categoryApi } from '@/api/category'
import { shopApi } from '@/api/shop'
import { 
  Plus, 
  Delete, 
  Edit,
  View,
  Folder,
  FolderOpened
} from '@element-plus/icons-vue'
