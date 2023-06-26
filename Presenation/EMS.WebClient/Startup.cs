using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(EMS.Webclient.Startup))]
namespace EMS.Webclient
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
