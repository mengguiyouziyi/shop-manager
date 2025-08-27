import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import { shopApi } from '@/api/shop'
import { categoryApi } from '@/api/category'
import { 
  Plus, 
  Delete, 
  Edit,
  View,
  Search,
  Refresh,
  Download,
  Upload,
  Setting,
  Shop
} from '@element-plus/icons-vue'
