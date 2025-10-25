# QCentroid Error: Invalid Azure Connection String

## 🔴 Error Summary

**Error Type:** `ValueError: Invalid connection string`

**Location:** Microsoft Azure Quantum provider configuration

**Cause:** QCentroid platform cannot connect to Azure Quantum workspace

---

## 🔍 What This Means

This error occurs **before** your solver runs. The QCentroid platform is trying to:
1. Configure the Microsoft Azure Quantum provider
2. Connect to an Azure Quantum workspace
3. But the Azure connection string is invalid or missing

**This is NOT a problem with your code!** This is a QCentroid platform configuration issue.

---

## 🛠️ Solutions

### **Solution 1: Contact QCentroid Support (Recommended)**

This is a platform-level configuration issue that QCentroid needs to fix.

**Action Steps:**
1. **Contact QCentroid support** immediately:
   - Email: support@qcentroid.xyz (or check their documentation)
   - Subject: `Azure Quantum Connection String Error - Team 9`
   - Body:
   ```
   Hello,

   We are Team 9 (c2_team9_singapore@qai-ventures.com) from GenQ - Singapore 2025.
   
   We're getting this error when trying to run our solver:
   "ValueError: Invalid connection string" in /problem/providers/microsoft.py
   
   Solver URN: dbs-fraud-qsvm-classifier
   Provider: Microsoft
   Device: IonQ Simulator
   
   The error occurs during Azure Quantum workspace configuration before our 
   solver code executes. Could you please verify the Azure connection string 
   is properly configured for our account?
   
   Error traceback:
   File "/problem/providers/microsoft.py", line 52, in create_config
       workspace = Workspace.from_connection_string(AZURE_CONNECTION_STRING)
   ValueError: Invalid connection string
   
   Thank you!
   Team 9
   ```

---

### **Solution 2: Verify Solver Configuration**

Check if you selected the wrong provider during solver registration.

**Verify in your solver registration:**
- **SDK:** Should be `Qiskit` ✅
- **Provider:** Should be `QCentroid` ✅ (NOT Microsoft)
- **Device:** IonQ Simulator or IonQ Forte 1

**If you selected "Microsoft" as provider:** This is the issue!
- Microsoft provider expects Azure Quantum workspace
- IonQ devices are accessed through QCentroid, not Microsoft

**Fix:**
1. Go to QCentroid solver management
2. Edit your solver: `dbs-fraud-qsvm-classifier`
3. Change **Provider** from `Microsoft` to `QCentroid`
4. Save changes
5. Try running again

---

### **Solution 3: Check Job Hardware Configuration**

When creating the job, verify you selected:

**Correct:**
- Provider: QCentroid
- Device: IonQ Simulator (free) or IonQ Forte 1

**Incorrect:**
- Provider: Microsoft Azure Quantum
- Device: Any Azure device

**Fix:**
1. Cancel current job
2. Create new job
3. Select **QCentroid** provider (not Microsoft)
4. Select IonQ Simulator or IonQ Forte 1
5. Submit job

---

### **Solution 4: Use Alternative Backend**

If the issue persists, try a different quantum backend temporarily.

**In your solver registration or job config, if there's an option:**
- Try using a different provider if available
- Or contact support to enable QCentroid-IonQ access

---

## 🔧 Quick Diagnostic Checklist

Check these in order:

- [ ] **Provider selection:** Did you select `QCentroid` (not Microsoft)?
- [ ] **Device selection:** Did you select IonQ Simulator or IonQ Forte 1?
- [ ] **Azure credentials:** Does QCentroid have valid Azure Quantum credentials?
- [ ] **Account permissions:** Is your team account authorized for Azure Quantum?
- [ ] **Platform issue:** Is this affecting all users or just your team?

---

## 📝 What You Should Do RIGHT NOW

### **Immediate Action:**

1. **Check solver registration:**
   ```
   Go to QCentroid → My Solvers → dbs-fraud-qsvm-classifier
   Verify: Provider = "QCentroid" (not "Microsoft")
   ```

2. **If Provider is wrong:**
   - Edit solver
   - Change Provider to `QCentroid`
   - Save
   - Retry job

3. **If Provider is correct:**
   - Contact QCentroid support (use email template above)
   - This is a platform configuration issue they need to fix
   - Mention you're part of GenQ - Singapore 2025 hackathon

4. **Alternative:**
   - Check if there's a "Provider" dropdown in job creation
   - Make sure it's set to use QCentroid/IonQ directly

---

## 🎯 Expected Behavior

**What SHOULD happen:**
```
1. Job submitted
2. QCentroid clones your GitHub repo
3. Installs dependencies
4. Configures IonQ quantum backend (through QCentroid)
5. Runs: python main.py
6. Your code connects to IonQ via QCentroid API
7. Results returned
```

**What's happening instead:**
```
1. Job submitted
2. QCentroid tries to configure Microsoft Azure provider
3. ❌ Fails because Azure connection string is invalid
4. Your solver never runs
```

---

## 🆘 Need Help?

This is likely a QCentroid platform configuration issue, not your code!

**Contact:**
- QCentroid Support: Check their documentation for support email
- Hackathon Organizers: They may have direct contact with QCentroid
- Your team's designated contact person

**What to tell them:**
- Error: "Invalid connection string" in Microsoft provider
- Solver: dbs-fraud-qsvm-classifier
- Team: c2_team9_singapore@qai-ventures.com
- Provider selected: QCentroid (or Microsoft if that's the issue)
- Device: IonQ Simulator

---

## 📊 Root Cause Analysis

**Most Likely Causes (in order):**

1. **Wrong provider selected** (70% probability)
   - You selected "Microsoft" instead of "QCentroid"
   - Fix: Change provider to QCentroid

2. **QCentroid platform misconfiguration** (20% probability)
   - QCentroid's Azure credentials expired or invalid
   - Fix: Contact QCentroid support

3. **Account permissions** (10% probability)
   - Your team account not authorized for Azure Quantum
   - Fix: Contact hackathon organizers

---

## ✅ After Fix

Once resolved, your solver should:
1. ✅ Clone successfully from GitHub
2. ✅ Install dependencies
3. ✅ Connect to IonQ Simulator/Forte 1
4. ✅ Execute quantum circuits
5. ✅ Return fraud detection results

Expected runtime: 15-30 minutes

---

## 📁 Save This Error Report

Keep this for reference when contacting support. Include:
- This document
- Full error traceback
- Your solver URN: `dbs-fraud-qsvm-classifier`
- Team email: `c2_team9_singapore@qai-ventures.com`

**Good luck resolving this! The issue is on the platform side, not your code.** 🚀
