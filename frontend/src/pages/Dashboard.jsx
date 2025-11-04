import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Users, TrendingUp, DollarSign, Star } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsRes, usersRes, subsRes] = await Promise.all([
        axios.get(`${API}/bot/stats`),
        axios.get(`${API}/bot/users`),
        axios.get(`${API}/bot/subscriptions`)
      ]);
      
      setStats(statsRes.data);
      setUsers(usersRes.data);
      setSubscriptions(subsRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      toast.error("Failed to fetch dashboard data");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-slate-600 font-medium">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Crypto Bot Dashboard
              </h1>
              <p className="text-slate-600 text-sm">Monitor your Telegram bot analytics</p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card data-testid="total-users-card" className="bg-white border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Total Users</CardTitle>
              <Users className="w-5 h-5 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">{stats?.total_users || 0}</div>
              <p className="text-xs text-slate-500 mt-1">Registered users</p>
            </CardContent>
          </Card>

          <Card data-testid="premium-users-card" className="bg-white border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Premium Users</CardTitle>
              <Star className="w-5 h-5 text-amber-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-amber-600">{stats?.premium_users || 0}</div>
              <p className="text-xs text-slate-500 mt-1">Active subscriptions</p>
            </CardContent>
          </Card>

          <Card data-testid="free-users-card" className="bg-white border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Free Users</CardTitle>
              <Users className="w-5 h-5 text-slate-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-700">{stats?.free_users || 0}</div>
              <p className="text-xs text-slate-500 mt-1">Free tier users</p>
            </CardContent>
          </Card>

          <Card data-testid="revenue-card" className="bg-white border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-slate-600">Total Revenue</CardTitle>
              <DollarSign className="w-5 h-5 text-emerald-600" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-emerald-600">${stats?.total_revenue || 0}</div>
              <p className="text-xs text-slate-500 mt-1">From subscriptions</p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs Section */}
        <Tabs defaultValue="users" className="space-y-6">
          <TabsList className="bg-white border border-slate-200 p-1">
            <TabsTrigger data-testid="users-tab" value="users" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              Users
            </TabsTrigger>
            <TabsTrigger data-testid="subscriptions-tab" value="subscriptions" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              Subscriptions
            </TabsTrigger>
            <TabsTrigger data-testid="setup-tab" value="setup" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white">
              Bot Setup
            </TabsTrigger>
          </TabsList>

          <TabsContent value="users">
            <Card className="bg-white border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>All Users</CardTitle>
                <CardDescription>List of all registered bot users</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-200">
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Telegram ID</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Username</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Name</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Tier</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Joined</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.length === 0 ? (
                        <tr>
                          <td colSpan="5" className="text-center py-8 text-slate-500">
                            No users yet. Share your bot link to get started!
                          </td>
                        </tr>
                      ) : (
                        users.map((user, index) => (
                          <tr key={index} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                            <td className="py-3 px-4 text-sm text-slate-900 font-mono">{user.telegram_id}</td>
                            <td className="py-3 px-4 text-sm text-slate-700">@{user.username || 'N/A'}</td>
                            <td className="py-3 px-4 text-sm text-slate-700">{user.first_name || 'N/A'}</td>
                            <td className="py-3 px-4">
                              {user.subscription_tier === 'premium' ? (
                                <Badge className="bg-amber-100 text-amber-700 border-amber-200">Premium</Badge>
                              ) : (
                                <Badge variant="outline" className="text-slate-600">Free</Badge>
                              )}
                            </td>
                            <td className="py-3 px-4 text-sm text-slate-600">
                              {new Date(user.created_at).toLocaleDateString()}
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="subscriptions">
            <Card className="bg-white border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Active Subscriptions</CardTitle>
                <CardDescription>Premium subscription details</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-200">
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">User ID</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Tier</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Started</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Expires</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {subscriptions.length === 0 ? (
                        <tr>
                          <td colSpan="5" className="text-center py-8 text-slate-500">
                            No subscriptions yet
                          </td>
                        </tr>
                      ) : (
                        subscriptions.map((sub, index) => {
                          const expiresAt = new Date(sub.expires_at);
                          const isActive = expiresAt > new Date();
                          return (
                            <tr key={index} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                              <td className="py-3 px-4 text-sm text-slate-900 font-mono">{sub.telegram_id}</td>
                              <td className="py-3 px-4">
                                <Badge className="bg-amber-100 text-amber-700 border-amber-200">Premium</Badge>
                              </td>
                              <td className="py-3 px-4 text-sm text-slate-600">
                                {new Date(sub.created_at).toLocaleDateString()}
                              </td>
                              <td className="py-3 px-4 text-sm text-slate-600">
                                {expiresAt.toLocaleDateString()}
                              </td>
                              <td className="py-3 px-4">
                                {isActive ? (
                                  <Badge className="bg-emerald-100 text-emerald-700 border-emerald-200">Active</Badge>
                                ) : (
                                  <Badge variant="outline" className="text-slate-600">Expired</Badge>
                                )}
                              </td>
                            </tr>
                          );
                        })
                      )}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="setup">
            <Card className="bg-white border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Bot Setup Instructions</CardTitle>
                <CardDescription>How to configure and run your Telegram bot</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">1. Get Your Telegram Bot Token</h3>
                  <p className="text-slate-600 mb-2">Talk to <a href="https://t.me/BotFather" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">@BotFather</a> on Telegram:</p>
                  <ul className="list-disc list-inside space-y-1 text-slate-600 ml-4">
                    <li>Send <code className="bg-slate-100 px-2 py-0.5 rounded text-sm">/newbot</code></li>
                    <li>Choose a name and username for your bot</li>
                    <li>Copy the token provided by BotFather</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">2. Get API Keys (Optional but Recommended)</h3>
                  <div className="space-y-3">
                    <div>
                      <p className="font-medium text-slate-700">CryptoPanic API (Crypto News)</p>
                      <p className="text-sm text-slate-600">Sign up at <a href="https://cryptopanic.com/developers/api/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">cryptopanic.com/developers/api</a></p>
                    </div>
                    <div>
                      <p className="font-medium text-slate-700">NewsAPI (Financial News)</p>
                      <p className="text-sm text-slate-600">Sign up at <a href="https://newsapi.org/" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">newsapi.org</a></p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">3. Configure Environment Variables</h3>
                  <p className="text-slate-600 mb-2">Add these to <code className="bg-slate-100 px-2 py-0.5 rounded text-sm">/app/backend/.env</code>:</p>
                  <div className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto">
                    <pre className="text-sm">
{`TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
EMERGENT_LLM_KEY=sk-emergent-fC6934eD2A55986A6A
CRYPTOPANIC_API_KEY=your_cryptopanic_key (optional)
NEWSAPI_KEY=your_newsapi_key (optional)`}
                    </pre>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">4. Run the Bot</h3>
                  <p className="text-slate-600 mb-2">Execute this command:</p>
                  <div className="bg-slate-900 text-slate-100 p-4 rounded-lg">
                    <code className="text-sm">python /app/backend/bot_service.py</code>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-blue-900">
                    <strong>💡 Note:</strong> The AI assistant uses the Emergent LLM key (already configured). 
                    News features will work with limited data without API keys, but for full functionality, add the optional API keys above.
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
