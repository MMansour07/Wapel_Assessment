using EMS.Service.Infrastructure;
using EMS.Webclient;
using System;
using System.Web.Mvc;
using System.Web.Optimization;
using System.Web.Routing;

namespace EMS.WebClient
{
    public class MvcApplication : System.Web.HttpApplication
    {
        [System.Obsolete]
        protected void Application_Start()
        {
            AreaRegistration.RegisterAllAreas();
            FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
            RouteConfig.RegisterRoutes(RouteTable.Routes);
            BundleConfig.RegisterBundles(BundleTable.Bundles);
            MappingProfile.Init();
            UnityConfig.RegisterComponents();
        }
        protected void Application_Error(object sender, EventArgs e)
        {
            //Server.ClearError();
            //Response.Redirect("~/Error");
        }
    }
}
