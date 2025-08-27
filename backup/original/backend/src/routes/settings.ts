import { Router } from 'express';
import { authenticateToken, requireRole } from '../middleware/auth';
import { 
  getSettings, 
  updateSettings, 
  backupData, 
  restoreData 
} from '../controllers/settingsController';

const router = Router();

router.get('/', authenticateToken, requireRole(['admin']), getSettings);
router.put('/', authenticateToken, requireRole(['admin']), updateSettings);
router.post('/backup', authenticateToken, requireRole(['admin']), backupData);
router.post('/restore', authenticateToken, requireRole(['admin']), restoreData);

export { router as settingsRouter };