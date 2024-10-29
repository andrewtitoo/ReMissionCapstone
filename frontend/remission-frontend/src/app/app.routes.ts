import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LoggerComponent } from './components/logger/logger.component';
import { BotComponent } from './components/bot/bot.component';

export const appRoutes: Routes = [
  { path: '', component: DashboardComponent },  // Default route to Dashboard
  { path: 'dashboard', component: DashboardComponent },
  { path: 'logger', component: LoggerComponent },
  { path: 'bot', component: BotComponent },
  { path: '**', redirectTo: '' }  // Redirect any unknown path to Dashboard
];
