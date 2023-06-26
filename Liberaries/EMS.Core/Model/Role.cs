using Microsoft.AspNet.Identity.EntityFramework;

namespace EMS.Core.Model
{
    public class Role : IdentityRole
    {
        public string Description { get; set; }
    }
}
