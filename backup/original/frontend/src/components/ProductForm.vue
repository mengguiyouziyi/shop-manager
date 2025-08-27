import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import { productApi } from '@/api/product'
import { categoryApi } from '@/api/category'
import { shopApi } from '@/api/shop'
import { 
  Plus, 
  Delete, 
  Upload, 
  Download,
  Picture,
  Edit,
  View,
  Link
} from '@element-plus/icons-vue'
