import { ref, reactive, onMounted, computed, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useRouter } from 'vue-router'
import { statisticsApi } from '@/api/statistics'
import { shopApi } from '@/api/shop'
import { 
  TrendCharts,
  PieChart,
  Histogram,
  DataLine,
  Download,
  Refresh,
  Setting,
  View
} from '@element-plus/icons-vue'
