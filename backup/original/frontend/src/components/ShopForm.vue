import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import { shopApi } from '@/api/shop'
import { categoryApi } from '@/api/category'
import { 
  Plus, 
  Delete, 
  Upload, 
  Download,
  Picture,
  Edit,
  View
} from '@element-plus/icons-vue'
