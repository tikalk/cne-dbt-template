{% macro  get_policy_type_pretty_names_mapping(tool_name, policy_type) %}
    case
        {# -- tenable-nessus-pro #}
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Advanced Scan' then 'Advanced Scan'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Internal PCI Network Scan' then 'Internal PCI Network Scan'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Policy Compliance Auditing' then 'Policy Compliance Auditing'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Copy of Advanced Scan' then 'Copy of Advanced Scan'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'VA Scan' then 'VA Scan'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Basic Network Scan' then 'Basic Network Scan'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Log4Shell' then 'Log4Shell'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'PCI Quarterly External Scan' then 'PCI Quarterly External Scan'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Web Application Tests' then 'Web Application Tests'
        when '{{ tool_name }}' = 'tenable-nessus-pro' and policy_type = 'Host Discovery' then 'Host Discovery'

        {# -- tenable-io #}
        WHEN '{{ tool_name }}' = 'tenable-io' AND policy_type = 'ps' THEN 'PS Scan'
        WHEN '{{ tool_name }}' = 'tenable-io' AND policy_type = 'remote' THEN 'Remote Scan'
        WHEN '{{ tool_name }}' = 'tenable-io' AND policy_type = 'agent' THEN 'Agent Scan'

        {# -- sentinel-one #}
        WHEN '{{ tool_name }}' = 'sentinel-one' AND policy_type = 'account' THEN 'Account'
        WHEN '{{ tool_name }}' = 'sentinel-one' AND policy_type = 'group' THEN 'Group'
        WHEN '{{ tool_name }}' = 'sentinel-one' AND policy_type = 'site' THEN 'Site'

        {# -- qualys-vmdr #}
        WHEN '{{ tool_name }}' = 'qualys-vmdr' AND policy_type = 'Vulnerability Scan' THEN 'Vulnerability Scan'

        {# -- panw-panorama #}
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: sdwan-saas-quality' THEN 'SD-WAN SaaS Quality Profile'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: sdwan-traffic-distribution' THEN 'SD-WAN Traffic Distribution Profile'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: sdwan-path-quality' THEN 'SD-WAN Path Quality Profile'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: virus' THEN 'Security Profile: Antivirus'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: file-blocking' THEN 'Security Profile: File Blocking'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: url-filtering' THEN 'Security Profile: URL filtering'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: vulnerability' THEN 'Security Profile: Vulnerability Protection'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: wildfire-analysis' THEN 'Security Profile: Wildfire Analysis'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: custom-url-category' THEN 'Security Profile: URL Category'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: data-filtering' THEN 'Security Profile: Data Filtering'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: data-objects' THEN 'Security Profile: Data Objects'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: hip-objects' THEN 'Security Profile: HIP Objects'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: hip-profiles' THEN 'Security Profile: HIP Profiles'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'templates' THEN 'Template'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: decryption' THEN 'Decryption Profile'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'template-stacks' THEN 'Template Stack'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'security-profiles: spyware' THEN 'Security Profile: Anti-Spyware'
        WHEN '{{ tool_name }}' = 'panw-panorama' AND policy_type = 'panorama-mgt-config' THEN 'Panorama Config'

        {# --panw-cortex #}
        WHEN '{{ tool_name }}' = 'panw-cortex' AND policy_type = 'restrictions' THEN 'Profile - Restrictions'
        WHEN '{{ tool_name }}' = 'panw-cortex' AND policy_type = 'exploit' THEN 'Profile - Exploit'
        WHEN '{{ tool_name }}' = 'panw-cortex' AND policy_type = 'policy' THEN 'policy'
        WHEN '{{ tool_name }}' = 'panw-cortex' AND policy_type = 'agent_settings' THEN 'Profile - Agent Settings'
        WHEN '{{ tool_name }}' = 'panw-cortex' AND policy_type = 'malware' THEN 'Profile - Malware'

        {# --okta #}
        WHEN '{{ tool_name }}' = 'okta' AND policy_type = 'MFA_ENROLL' THEN 'MFA Enroll'
        WHEN '{{ tool_name }}' = 'okta' AND policy_type = 'OKTA_SIGN_ON' THEN 'Sign On'
        WHEN '{{ tool_name }}' = 'okta' AND policy_type = 'PASSWORD' THEN 'Password'

        {# --msft-purview #}
        WHEN '{{ tool_name }}' = 'msft-purview' AND policy_type = 'Hold' THEN 'Retention'
        WHEN '{{ tool_name }}' = 'msft-purview' AND policy_type = 'InsiderRisk' THEN 'Insider Risk'
        WHEN '{{ tool_name }}' = 'msft-purview' AND policy_type = 'Dlp' THEN 'Data Loss Protection (DLP)'
        WHEN '{{ tool_name }}' = 'msft-purview' AND policy_type = 'AutoLabeling' THEN 'Auto Labeling'
        WHEN '{{ tool_name }}' = 'msft-purview' AND policy_type = 'ProtectionAlert' THEN 'Protection Alert'

        {# --msft-office365 #}
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'anti-malware' THEN 'Anti-Malware'
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'atppolicyforo365' THEN 'Atp-Office365'
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'dkimsigningconfig' THEN 'Dkim Signing Config'
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'safe-links' THEN 'Safe Links'
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'anti-spam-outbound' THEN 'Anti-Spam Outbound'
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'safe-attachments' THEN 'Safe Attachments'
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'anti-phishing' THEN 'Anti-Phishing'
        WHEN '{{ tool_name }}' = 'msft-office365' AND policy_type = 'anti-spam-inbound' THEN 'Anti-Spam Inbound'

        {# --msft-intune #}
        WHEN '{{ tool_name }}' = 'msft-intune' AND policy_type = 'endpointSecurity' THEN 'Endpoint Security'
        WHEN '{{ tool_name }}' = 'msft-intune' AND policy_type = 'deviceConfiguration' THEN 'Device Configuration'

        {# --msft-aad #}
        WHEN '{{ tool_name }}' = 'msft-aad' AND policy_type = 'ConditionalAccess' THEN 'Conditional Access Policy'

        {# --jamf-pro #}
        WHEN '{{ tool_name }}' = 'jamf-pro' AND policy_type = 'profile' THEN 'Configuration Profile'
        WHEN '{{ tool_name }}' = 'jamf-pro' AND policy_type = 'policy' THEN 'Policy'

        {# --cyberark-epm #}
        WHEN '{{ tool_name }}' = 'cyberark-epm' AND policy_type = 'default-policy' THEN 'Default Policy'
        WHEN '{{ tool_name }}' = 'cyberark-epm' AND policy_type = 'agent-configurations' THEN 'Agent Configuration'
        WHEN '{{ tool_name }}' = 'cyberark-epm' AND policy_type = 'privilege-threat-protection' THEN 'Privilege Threat Protection'

        {# --crowdstrike-falcon #}
        WHEN '{{ tool_name }}' = 'crowdstrike-falcon' AND policy_type = 'prevention' THEN 'Prevention'
        WHEN '{{ tool_name }}' = 'crowdstrike-falcon' AND policy_type = 'device_control' THEN 'Device Control'

        {# --cloudflare #}
        WHEN '{{ tool_name }}' = 'cloudflare' AND policy_type = 'account' THEN 'Account'

        {# --zscaler-zia #}
        WHEN '{{ tool_name }}' = 'zscaler-zia' AND policy_type = 'fw_filtering_rule' THEN 'Firewall Filtering Rule'
        WHEN '{{ tool_name }}' = 'zscaler-zia' AND policy_type = 'url_filtering_rule' THEN 'URL Filtering Rule'

        {# --msft-sccm #}
        WHEN '{{ tool_name }}' = 'msft-sccm' AND policy_type = 'SettingsAndPolicy:SMS_AdvancedThreatProtectionSettings' THEN 'Windows Defender Advanced Threat Protection Settings'
        WHEN '{{ tool_name }}' = 'msft-sccm' AND policy_type = 'AntiMalware' THEN 'Anti-Malware Policies'
        WHEN '{{ tool_name }}' = 'msft-sccm' AND policy_type = 'SettingsAndPolicy:SMS_ExploitGuardSettings' THEN 'Windows Defender Exploit Guard Policies'
        WHEN '{{ tool_name }}' = 'msft-sccm' AND policy_type = 'SettingsAndPolicy:SMS_FirewallSettings' THEN 'Windows Defender Firewall Policies'
        WHEN '{{ tool_name }}' = 'msft-sccm' AND policy_type = 'SettingsAndPolicy:SMS_CompliancePolicySettings' THEN 'Windows Defender Compliance Policies'

        ELSE ''
    end
{% endmacro %}
