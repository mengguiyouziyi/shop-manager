import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import { productApi } from '@/api/product'
import { orderApi } from '@/api/order'
import { memberApi } from '@/api/member'
import { shopApi } from '@/api/shop'
import { 
  Plus, 
  Delete, 
  Search,
  Refresh,
  Printer,
  Download,
  ShoppingCart,
  Money,
  CreditCard,
  Wallet
} from '@element-plus/icons-vue'
