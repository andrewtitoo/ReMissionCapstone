import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LoggerComponent } from './components/logger/logger.component';
import { BotComponent } from './components/bot/bot.component';

export const routes: Routes = [
  { path: 'dashboard', component: DashboardComponent },
  { path: 'logger', component: LoggerComponent },
  { path: 'bot', component: BotComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: '**', redirectTo: '/dashboard' } // Fallback for unknown paths
];
